# Political_Party_Polarization

Party Polarization in the United States Congress

A Report by Alexandra Schein
May 14th, 2019

*America has seen growing polarization between the Republican and Democratic parties over the last 40-50 years. In this report, I analyze voting trends between differing parties across the 95th to 116th United States Congresses*.

Data used: Lewis, Jeffrey B., Keith Poole, Howard Rosenthal, Adam Boche, Aaron Rudkin, and Luke Sonnet (2019). Voteview: Congressional Roll-Call Votes Database. https://voteview.com/

##DATA

Using the extensive data provided by Keith Poole and Howard Rosenthal, I look at the congressional roll call vote in American history. I use two data sets; the first set includes every vote taken by every member in the selected congresses, and the second consists of basic biographical information for every member, particularly name and party. I limit the data to the House members, disregarding senate votes. I also limit the research to the 95th to the 116th (current congress). With this data, I am able to track every member’s voting trend for a given congress, and thus, how these trends change over time. By considering voting trends in congress over the last 42 years, one can analyze polarization based on how partisan or bipartisan each congress voted overall.

I create political networks for each congress where the nodes are every House member in the congress and the edges reflect similar voting between two congresspeople . Given how divided the democratic and republican parties in the United States are today, and particularly how strong inter-party cohesion has become, I compare democratic to republican votes. Thus, to look at inter-party cooperation on roll-call votes, I exclusively evaluate connections between republican and democratic nodes, i.e. House members with these party affiliations.

##THRESHOLD

Every member in congress is likely to vote the same as a member of the opposing party at some point, creating a fully connected network. To avoid this discrepancy, I use a threshold that each pair of members’ voting records must meet in order for an edge to be created; each pair of congresspeople must vote the same on a specific number of bills for them to be connected. To find this value, I create a network of a single congress and find its average degree for different threshold values. Since voting patterns can change drastically over 42 years, I tested these values for both the 95th and 116th congresses (Page 4).

From these graphs, we see that the median value for the 95th congress is 0.5 while the median value for the 116th congress is around 0.35. To have an adequate threshold across all 21 congresses, I use a threshold of 0.4.

To create an edge between two congresspeople, I take the fraction of votes where they voted the same on a given roll over the number of same rolls they voted on, not necessarily sharing the same vote. If this value is greater than the threshold, an edge is created.



##Degree Measures

Since each network is exclusively composed of inter-party connections, nodes with high degree centrality have a higher rate of voting the same as members of the opposing party. I evaluate the average degree, <k>, of every network. Congresses with a high <k> reflect more bipartisan voting while congresses with low <k> suggest greater party-voting disparity. I plot the average degree of congresses to analyze how voting trends have changed, based on party affiliation.
Analysis

The figure above displays the average degree as a function of congress. I look at the 95th to 116th congresses, ticked with the corresponding year that the specified congress begins. Congresses with high <k>, such as the 107th, reflects more bipartisan voting within the House while the 114th congress shows the lowest degree, meaning very few republicans shared similar voting records to those of democrats. This visualization demonstrates significant voting trends. Despite my prediction that <k> would decline steadily over time, we see a general fluctuation. However, when considering acting presidents and events during certain time periods, this figure is very telling.

The most striking drop in voting similarities occurs in 111th Congress, beginning in 2009, which is also the first year of Barack Obama’s presidency. We see the highest centrality at the 107th congress. This could be due to the fact that 2001 was the year of 9/11, which infused a collective trauma in America and increased patriotism. Considering presidencies across the 21 congresses, there is a trend of the highest bipartisan voting in the first term of the president at the time. For instance, Reagan’s presidency spans the 97th to the 101st congress with the highest <k> in his first term. George Bush’s presidency begins in 1989 where the highest <k> is in his first term during the 101st congress. George W. Bush’ presidency begins in the 107th congress, with the highest <k> in the network, and continues to decline. This is the case for all presidents besides Bill Clinton in 1993 to 2001 and Donald Trump, beginning in 2017. Ultimately, degree centrality is a significant measure to study the changing political climate.
